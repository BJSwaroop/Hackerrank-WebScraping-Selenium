import { Component } from '@angular/core';
import { ContentServiceService } from '../content-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-hackerrank-plagiarism-check',
  templateUrl: './hackerrank-plagiarism-check.component.html',
  styleUrls: ['./hackerrank-plagiarism-check.component.scss']
})
export class HackerrankPlagiarismCheckComponent {
  constructor(private router: Router) { 
  }
  fetchUsersData(){
    this.router.navigate(['/usersAttempts']);
  }
}
