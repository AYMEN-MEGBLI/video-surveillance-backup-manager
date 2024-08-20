import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.development';

export interface TimeRange extends Array<number> {
  start: number;
  end: number;
}
export interface MotionData {
  humains: TimeRange[];
  animaux: TimeRange[];
  vehicules: TimeRange[];
  autres: TimeRange[];
}




@Injectable({
  providedIn: 'root'
})



export class VideoService {


  
  constructor(private http: HttpClient) {}

  private baseUrl = environment.baseUrl 

  getMotionData(videoPath: string): Observable<MotionData> {
   let full_url=`${this.baseUrl}/motion-data?file_name=${videoPath.replaceAll(" ","_")}`
   console.log(full_url)
    return this.http.get<MotionData>(full_url);
  }

  file_exists(fileName : string){
    console.log(`/file-exists?file_name=${ fileName.replaceAll(" ","_") }`)
    return this.http.get<{ exists: boolean }>(`${this.baseUrl}/file-exists?file_name=${ fileName.replaceAll(" ","_") }`);
  }
  uploadFile(file: File): Observable<any> {
    
    const formData = new FormData();
    formData.append('file', file, (file.name).replaceAll(" ","_"));
    console.log("url posst ",formData)
    return this.http.post<any>(`${this.baseUrl}/upload/`, formData);
  }

get_videos_details(){
  let full_url=`${this.baseUrl}/videos`
  console.log(full_url)
  return this.http.get<any>(full_url);
}
  
}
  