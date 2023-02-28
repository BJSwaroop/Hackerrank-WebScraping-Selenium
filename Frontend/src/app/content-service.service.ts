import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ContentServiceService {

  constructor(private http: HttpClient) { }

  fetch_users_data(data:any): Observable<any>{
      console.log("HE", data);
      return this.http.post<any>(`http://127.0.0.1:8000/fetchUsers/`,data).pipe();
  }
}
