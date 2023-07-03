import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ContentServiceService {

  constructor(private http: HttpClient) { }
  userData: any;
  adminInfo:any;
  plagiarismData: any;
  checkPlagiarism(username: string): Observable<any>{
      // console.log("HE", data);
      this.http.post<any>(`http://127.0.0.1:8000/checkplagiarism/`,username).subscribe(
        response => {
          // Handle the response data here
          console.log(response);
          this.plagiarismData = response;
        },
        error => {
          // Handle any errors here
          console.error(error);
        }
        );
      return this.plagiarismData;
  };
  fetch_latest_attempts(): Observable<any>{
      // console.log("HE", data);
      this.http.post<any>(`http://127.0.0.1:8000/fetchlatest/`,this.adminInfo).subscribe(
        response => {
          // Handle the response data here
          this.userData = response;
          console.log(response);
        },
        error => {
          // Handle any errors here
          console.error(error);
        }
      );
      return this.userData;
  };
  fetch_old_attempts(): Observable<any>{
    console.log(this.adminInfo);
    this.http.post<any>(`http://127.0.0.1:8000/fetchold/`,this.adminInfo).subscribe(
      response => {
        // Handle the response data here
        this.userData = response;
        console.log(response);
      },
      error => {
        // Handle any errors here
        console.error(error);
      }
    );
    return this.userData;
    // console.log(this.userData); 
    // return this.userData;
  }
}
