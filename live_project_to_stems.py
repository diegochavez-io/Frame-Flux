import os
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.control_surface import ControlSurface
from ableton.v2.control_surface import MIDI_NOTE_TYPE

class BatchExport(ControlSurface):

    export_button = ButtonControl()

    def __init__(self, *a, **k):
        super(BatchExport, self).__init__(*a, **k)
        self._project_folder = "/path/to/project/folder"
        self._export_folder = "/path/to/export/folder"

    def export_projects(self):
        # Loop through each project file in the folder
        for project_file in os.listdir(self._project_folder):
            if project_file.endswith(".als"):
                # Open the project file
                self.song().load_song(os.path.join(self._project_folder, project_file))
                
                # Wait for the project to load
                self.wait(5000)  # Wait for 5 seconds
                
                # Loop through each track in the project
                for track in self.song().tracks:
                    # Solo the track
                    track.solo = True
                    
                    # Export the audio for the track
                    self.song().export_audio(self._export_folder, warp=True)
                    
                    # Wait for the export to complete
                    self.wait(10000)  # Wait for 10 seconds
                    
                    # Un-solo the track
                    track.solo = False

    @export_button.pressed
    def export_button(self, _):
        self.export_projects()
