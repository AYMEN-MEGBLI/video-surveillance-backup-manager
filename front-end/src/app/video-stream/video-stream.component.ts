import {  Component, ViewChild } from '@angular/core';
import { VdStreamService } from '../services/vd-stream.service';

@Component({
  selector: 'app-video-stream',
  templateUrl: './video-stream.component.html',
  styleUrls: ['./video-stream.component.scss']
})
export class VideoStreamComponent   {
  //vd_src = "http://127.0.0.1:8000/video_feed";
  vd_src = "assets/cam.jpg"
  defaultImage = 'assets/cam.jpg';
  isImageLoaded = false;
  @ViewChild('start_rec') start_rec: any;
  @ViewChild('stop_rec') stop_rec: any;
  @ViewChild('enable_or_diable') enable_or_diable: any;

  constructor(private videoStreamService: VdStreamService) {}


  onImageLoad() {
    this.isImageLoaded = true;
    this.vd_src="http://127.0.0.1:8000/video_feed"
    
  }

  onImageError() {
    console.error('Failed to load the image.');
    this.isImageLoaded = false;
    this.vd_src = this.defaultImage;
}
startRecording() {
  this.start_rec.nativeElement.disabled = true;
  this.stop_rec.nativeElement.disabled = false;

  this.videoStreamService.startRecording(0)
    .subscribe({
      next: response => {
        console.log('Recording started', response);
      },
      error: error => {
        console.error('Error starting recording', error);
      }
    });
}


stopRecording() {
  this.stop_rec.nativeElement.disabled = true;
  this.start_rec.nativeElement.disabled = false;
  this.videoStreamService.stopRecording()
    .subscribe({
      next: response => {
        console.log('Recording stopped', response);
      },
      error: error => {
        console.error('Error stopping recording', error);
      }
    });
}
enableOrDiable(){
  this.enable_or_diable.nativeElement.disabled = true;
  // if(this.isImageLoaded ) 
  //   this.vd_src = "assets/cam.jpg";
  // else
  //   this.vd_src="http://127.0.0.1:8000/video_feed";

  this.isImageLoaded = ! this.isImageLoaded;
  this.videoStreamService.enableOrDiable()
    .subscribe({
      next: response => {
        console.log('Recording stopped', response);
      },
      error: error => {
        console.error('Error stopping recording', error);
      }
    });
    
    this.enable_or_diable.nativeElement.disabled = false;
}



}