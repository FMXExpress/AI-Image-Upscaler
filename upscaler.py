import os
import replicate
import urllib.request
import hashlib
from delphifmx import *
import threading  # To handle background process without blocking the app

# Set the API token for Replicate
os.environ["REPLICATE_API_TOKEN"] = "replicate_com_api_key"

class ImageUpscalerApp(Form):

    def __init__(self, owner):
        # Setting up the style and form properties
        self.stylemanager = StyleManager(self)
        self.stylemanager.SetStyleFromFile("Air.style")

        self.SetProps(Caption="Image Upscaler + Replicate API", OnShow=self.__form_show, OnClose=self.__form_close)

        # Layout for the top components (Button and Label)
        self.layout_top = Layout(self)
        self.layout_top.SetProps(Parent=self, Align="Top", Height="50", Margins=Bounds(RectF(3, 3, 3, 3)))

        # Label to prompt the user
        self.prompt_label = Label(self)
        self.prompt_label.SetProps(Parent=self.layout_top, Align="Left", Text="Upload an Image:", Position=Position(PointF(20, 20)), Margins=Bounds(RectF(3, 3, 3, 3)))

        # Button to trigger file upload
        self.upload_button = Button(self)
        self.upload_button.SetProps(Parent=self.layout_top, Align="Right", Text="Select", Position=Position(PointF(290, 18)), Width=120, OnClick=self.__upload_image, Margins=Bounds(RectF(3, 3, 3, 3)))

        # Image control for the original image display
        self.img_original = ImageControl(self)
        self.img_original.SetProps(Parent=self, Align="Left", Position=Position(PointF(20, 60)), Width=300, Height=300, Margins=Bounds(RectF(3, 3, 3, 3)))

        # Image control for the upscaled image display
        self.img_upscaled = ImageControl(self)
        self.img_upscaled.SetProps(Parent=self, Align="Client", Position=Position(PointF(340, 60)), Width=300, Height=300, Margins=Bounds(RectF(3, 3, 3, 3)))

        # Status bar at the bottom
        self.status_bar = Label(self)
        self.status_bar.SetProps(Parent=self, Align="Bottom", Text="Status: Ready", Height=30, Margins=Bounds(RectF(3, 3, 3, 3)))

        # Timer for updating the status periodically
        self.timer = Timer(self)
        self.timer.Interval = 1000  # Timer event will trigger every second
        self.timer.Enabled = False
        self.timer.OnTimer = self.__on_timer_tick

        # Initialize variables for prediction handling
        self.prediction = None
        self.original_image_path = None

    def __form_show(self, sender):
        self.SetProps(Width=700, Height=400)

    def __form_close(self, sender, action):
        self.timer.Enabled = False
        action = "caFree"

    def __upload_image(self, sender):
        self.timer.Enabled = False

        open_dialog = OpenDialog(self)  # Create the OpenDialog instance
        open_dialog.Filter = "Image Files|*.png;*.jpg;*.jpeg"  # Filter to show only image files
        open_dialog.Title = "Select an Image"  # Set title of the dialog

        if open_dialog.Execute():  # If the user selects a file and clicks OK
            file_path = open_dialog.FileName  # Get the selected file path
            self.original_image_path = file_path
            self.img_original.LoadFromFile(file_path)
            self.status_bar.Text = "Status: Uploading and processing image..."
            self.upload_button.Enabled = False  # Disable upload button during processing
            #threading.Thread(target=self.__start_upscale, args=(file_path,)).start()  # Run upscale in background
            Application.ProcessMessages()
            self.__start_upscale(file_path)

    def __start_upscale(self, file_path):
        try:
            # Use Replicate's async process to handle the upscaling
            model = replicate.models.get("philz1337x/clarity-upscaler")
            version = model.versions.get("dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e")
            self.prediction = replicate.predictions.create(
                version=version,
                input={"image": open(file_path, "rb")}
            )
            self.timer.Enabled = True  # Enable the timer to start checking the status
        except Exception as e:
            self.status_bar.Text = f"Status: Error occurred - {str(e)}"
            self.upload_button.Enabled = True  # Re-enable the upload button

    def __on_timer_tick(self, sender):
        if self.prediction is None:
            return

        try:
            self.prediction.reload()  # Reload status periodically
            if self.prediction.status == "processing":
                # Split the log data into lines using \n as the delimiter
                lines = self.prediction.logs.strip().split('\n')
                # Get the last line
                status = lines[-1] if lines else self.prediction.status  # Ensure there is a valid line
                self.status_bar.Text = f"Status: {status}..."

            elif self.prediction.status in ["succeeded", "failed", "canceled"]:
                self.timer.Enabled = False  # Disable the timer when the process finishes
                if self.prediction.status == "succeeded":
                    image_url = self.prediction.output[0]  # Assuming the first output is the URL
                    file_name = './' + hashlib.md5(image_url.encode()).hexdigest() + '.png'
                    urllib.request.urlretrieve(image_url, file_name)

                    # Display the upscaled image
                    self.img_upscaled.LoadFromFile(file_name)
                    self.status_bar.Text = "Status: Upscaling complete!"
                else:
                    self.status_bar.Text = f"Status: Upscaling failed with status: {self.prediction.status}"
                self.upload_button.Enabled = True  # Re-enable the upload button
        except Exception as e:
            self.status_bar.Text = f"Status: Error occurred - {str(e)}"
            self.timer.Enabled = False
            self.upload_button.Enabled = True  # Re-enable the upload button

def main():

    Application.Initialize()
    Application.Title = "Image Upscaler + Replicate API"
    Application.MainForm = ImageUpscalerApp(Application)
    Application.MainForm.Show()
    Application.Run()
    Application.MainForm.Destroy()

if __name__ == '__main__':
    main()
