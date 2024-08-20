import { Component, ElementRef, ViewChild, OnDestroy, EventEmitter, Output } from '@angular/core';
import { MotionData, VideoService } from '../services/video.service';
import { Subscription, firstValueFrom } from 'rxjs';
@Component({
  selector: 'app-detection-from-video',
  templateUrl: './detection-from-video.component.html',
  styleUrls: ['./detection-from-video.component.scss']
})
export class DetectionFromVideoComponent  {
  videoUrl: string = '';
  @ViewChild('fileInput') fileInput: ElementRef = new ElementRef(null);
  private subscriptions: Subscription[] = [];
  public motionData!: MotionData | null ;
  public fileName!: string;
  selectedFile: File | null = null;
  uploadResponse: string | null = null;
  motionLoading : boolean =false ;
  uploadLoading : boolean =false ;
  fileExists : boolean =false ;

  constructor(private videoService: VideoService) {}

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
  
    if (input.files && input.files[0]) {
      
      this.selectedFile = input.files[0];
      this.videoUrl = URL.createObjectURL(this.selectedFile);
      this.fileName = this.selectedFile.name;
  
      try {
        // Check if the file exists
        const exists = await this.checkFile(this.fileName);
        
        console.log('File exists:', exists);
  
        if (exists) {
          console.log("File already exists:", exists);
          this.fileExists=true;
          this.uploadResponse = `File already exists: ${this.fileName}`;
           this.loadMotionData(this.fileName);
        } else {
          this.fileExists=false;
          this.uploadLoading=true;
          await this.uploadFile();
          this.uploadLoading=false; 
          console.log('File uploaded successfully');
          this.loadMotionData(this.fileName);
          this.motionData=null;
          
        }
       
      } catch (error : any) {
        this.uploadResponse = `Error: ${error.message}`;
      }
    }
  }

  async uploadFile(): Promise<void> {
    this.videoService.file_exists(this.fileName).subscribe((data : any ) => { 
      if (data && data.exists) {
        this.uploadResponse = `File already exists: ${this.fileName}`;
        
      }
    });
   
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile, this.selectedFile.name);

      try {
        const data = await firstValueFrom(this.videoService.uploadFile(this.selectedFile));
        if (data.error) {
          throw new Error(data.error);
        } else {
          this.uploadResponse = `File uploaded successfully: ${data.filename}`;
        }
      } catch (error: any) {
        throw new Error(`File upload failed: ${error.message}`);
      }
    } 
    
    
    else {
      this.uploadResponse = 'Please select a file first.';
    }
  }

  loadMotionData(fileName: string) {
    this.fileInput.nativeElement.disabled = true;
    this.motionLoading=true; 
    let motion_data_sub = this.videoService.getMotionData(fileName).subscribe((data) => {
      console.log(data);
      this.fileInput.nativeElement.disabled = false;
      this.motionData = data;
      this.motionLoading=false;
    });
    this.subscriptions.push(motion_data_sub);
  }


async checkFile(fileName: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.videoService.file_exists(fileName).subscribe({
        next: (data: any) => resolve(data.exists),
        error: (err) => reject(err)
      });
    });
  }
  


  ngOnDestroy() {
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }

}
