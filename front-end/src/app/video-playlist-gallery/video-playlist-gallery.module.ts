import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { VideoPlaylistGalleryRoutingModule } from './video-playlist-gallery-routing.module';
import { VideoPlaylistGalleryComponent } from './video-playlist-gallery.component';
import { DetectionFromVideoModule } from '../detection-from-video/detection-from-video.module';


@NgModule({
  declarations: [
    VideoPlaylistGalleryComponent,
    
  ],
  imports: [
    CommonModule,
    VideoPlaylistGalleryRoutingModule,
    DetectionFromVideoModule
   
  ]
})
export class VideoPlaylistGalleryModule { }
export interface VideoMetadata {
  file_name: string;
  date: string;
  duration: number;
  camera: number;
  categorized_objects: any; 
}