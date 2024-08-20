import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { VideoService } from '../services/video.service';

@Component({
  selector: 'app-upload-videoto-back-end',
  templateUrl: './upload-videoto-back-end.component.html',
  styleUrls: ['./upload-videoto-back-end.component.scss']
})
export class UploadVideotoBackEndComponent {



  selectedFile: File | null = null;
  uploadResponse: string | null = null;
  constructor(private videoService: VideoService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  uploadFile() {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile, this.selectedFile.name);

      this.videoService.uploadFile(this.selectedFile).subscribe({
        next: (data) => {
          if (data.error) {
          }
          this.uploadResponse = `File uploaded successfully: ${data.filename}`;
        },
        error: (error) => {
          this.uploadResponse = `File upload failed: ${error.message}`;
        }
      });
    } else {
      this.uploadResponse = 'Please select a file first.';
    }
  }

}
