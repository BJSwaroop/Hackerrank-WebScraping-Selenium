import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ContentServiceService } from '../content-service.service';
// import { UsersAttemptsComponent } from '../users-attempts/users-attempts.component';
@Component({
  selector: 'app-hackerrank-plagiarism-check',
  templateUrl: './hackerrank-plagiarism-check.component.html',
  styleUrls: ['./hackerrank-plagiarism-check.component.scss']
})
export class HackerrankPlagiarismCheckComponent {


  
  username: string = '';
  password: string = '';
  contestName: string = '';
  data: any;
  userData$: any;
  constructor(private router: Router,private contentService: ContentServiceService) { 
  }
  fetchUsersData(){
    this.data= {
      username: this.username,
      password: this.password,
      contest: this.contestName
    }
    this.contentService.adminInfo = this.data;
    this.router.navigate(['/usersAttempts']);
  }
}
