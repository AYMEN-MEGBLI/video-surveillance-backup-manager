import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { VideoPlaylistGalleryModule } from './video-playlist-gallery/video-playlist-gallery.module';
import { FormsModule } from '@angular/forms';
import { DetectionFromVideoModule } from './detection-from-video/detection-from-video.module';
import { MainComponent } from './main/main.component';
import { SettingComponent } from './setting/setting.component';
import { VideoStreamComponent } from './video-stream/video-stream.component';
import { InvalidPageComponent } from './invalid-page/invalid-page.component';
import { SideBarComponent } from './side-bar/side-bar.component';


@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    SettingComponent,
    VideoStreamComponent,
    InvalidPageComponent,
    SideBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    VideoPlaylistGalleryModule,
    DetectionFromVideoModule,
    FormsModule,


  
  ],
  
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

