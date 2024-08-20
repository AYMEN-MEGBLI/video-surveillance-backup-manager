import { Component, ElementRef, ViewChild, OnDestroy, EventEmitter, Output, OnInit, Renderer2 } from '@angular/core';
import { MotionData, VideoService } from './services/video.service';
import { Subscription, firstValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment.development';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  @ViewChild('menuBtn', { static: true }) menuBtn!: ElementRef;
  @ViewChild('sidebar', { static: true }) sidebar!: ElementRef;
  @ViewChild('container', { static: true }) container!: ElementRef;

  constructor(private renderer: Renderer2) {}

  isSidebarOpen = false;

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }
  }





