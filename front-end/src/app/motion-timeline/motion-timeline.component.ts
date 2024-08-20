import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges, ViewChild } from '@angular/core';

@Component({
  selector: 'app-motion-timeline',
  templateUrl: './motion-timeline.component.html',
  styleUrls: ['./motion-timeline.component.scss']
})
export class MotionTimelineComponent implements OnChanges {
  @Input() motionData: any = [];
@Input() VideoDuration  : number =60 ;
  
  @Output() seek = new EventEmitter<number>();
Object: any;

  ngOnChanges(changes: SimpleChanges) {
    if (changes['motionData']) {
      console.log('Motion data changed:', changes['motionData'].currentValue);
      this.a ={"loading...":[[0,0]]
      }
    }
    if (changes['VideoDuration'] ){
      console.log('VideoDuration changed:', changes['VideoDuration'].currentValue);
     

    }
    this.updateTimeline();
  }

  updateTimeline() {

    console.log('Updating timeline with motion data:', this.motionData);
 this.a = this.motionData;
    
    

  }

  calculatePosition(time: number): number {
    // Convert time to percentage of the total video length
    // Assuming total length is known or passed as an input
    const totalLength = this.VideoDuration || 100 ; // Replace with actual total length
    return (time / totalLength) * 100;
  }

  calculateWidth(start: number, end: number): number {
    // Convert time range to percentage width
 
    const totalLength =  this.VideoDuration || 100 // Replace with actual total length
    return ((end - start) / totalLength) * 100;
  }

  seekTo(position: number) {
    this.seek.emit(position);
  }
  colors=["#76c789","blue"," #76c7c0","yellow"];
 
  public a ={"loading...":[[0,0]]} 
 
  ;}