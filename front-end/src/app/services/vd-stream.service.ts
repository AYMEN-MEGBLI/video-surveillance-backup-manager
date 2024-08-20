import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class VdStreamService {
  private baseUrl = environment.baseUrl  // URL de base de l'API

  constructor(private http: HttpClient) {}

  startRecording(fileName: string | number): Observable<any> {
    return this.http.get(`${this.baseUrl}/start-recording`);
  }

  stopRecording(): Observable<any> {
     return this.http.get(`${this.baseUrl}/stop-recording`);
  }
  enableOrDiable(): Observable<any> {
    return this.http.get(`${this.baseUrl}/enable-disable`);
  }
  
}
