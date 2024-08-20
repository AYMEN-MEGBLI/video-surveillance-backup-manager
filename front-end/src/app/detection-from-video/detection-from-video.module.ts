import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DetectionFromVideoRoutingModule } from './detection-from-video-routing.module';
import { DetectionFromVideoComponent } from './detection-from-video.component';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { MotionTimelineComponent } from '../motion-timeline/motion-timeline.component';

@NgModule({
  declarations: [
    DetectionFromVideoComponent,
    VideoPlayerComponent,
    MotionTimelineComponent
   
  ],
  imports: [
    CommonModule,
    DetectionFromVideoRoutingModule,
    
  ]
  ,
  exports:[MotionTimelineComponent]
})
export class DetectionFromVideoModule { }
