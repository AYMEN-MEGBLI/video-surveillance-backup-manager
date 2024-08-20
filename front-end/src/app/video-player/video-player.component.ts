import { Component, Input, ViewChild, ElementRef, OnChanges, SimpleChanges, AfterViewInit } from '@angular/core';
import videojs from 'video.js';
import Player from "video.js/dist/types/player";
import { MotionData } from '../services/video.service';

@Component({
  selector: 'app-video-player',
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.scss']
})
export class VideoPlayerComponent implements OnChanges, AfterViewInit {
  @Input() videoUrl ! : string | null ;
  @Input() motionData!: MotionData | null;
  @ViewChild('videoPlayer') videoPlayer!: ElementRef<HTMLVideoElement>;
  player!: Player;
  vdDuration: number = 0;

  ngAfterViewInit() {
    this.initializePlayer();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['videoUrl'] && this.videoUrl) {
      this.updateVideoSource();
    }

    if (changes['motionData']) {
      this.updateMotionData();
    }
  }

  initializePlayer() {
  
    if (this.videoPlayer) {
      this.player = videojs(this.videoPlayer.nativeElement, {
        autoplay: true,
        className: "video-js vjs-sea ",
        preload: 'auto',
       width: 1024,
        height: 576,
        controls: true

      });

      this.player.on('loadedmetadata', () => {
        this.vdDuration = this.player.duration() || 0;
        console.log('loadedmetadata', this.vdDuration);
      });
    }
  }

  updateVideoSource() {
    if (this.player && this.videoUrl) {
      console.log('Updating video source:', this.videoUrl);
      this.player.src({ src: this.videoUrl, type: 'video/mp4' });
      this.player.load();

      // Ensure to update the duration once the metadata is loaded
      this.player.one('loadedmetadata', () => {
        this.vdDuration = this.player.duration() || 0;
        console.log('loadedmetadata', this.vdDuration);
      });
    }
  }

  updateMotionData() {
    // Update motion data here
  this.motionData = this.motionData;
  }

  onTimeUpdate(event: Event) {
    const currentTime = this.player.currentTime();
    // Handle time update
  }

  onSeek(position: number) {
    this.player.currentTime(position);
    this.player.play();
  }
  extraireSequence(start: number, end: number) {
    const startTime = start.toFixed(2);
    const endTime = end.toFixed(2);
    const videoElement = this.videoPlayer.nativeElement;
    
  }
}

