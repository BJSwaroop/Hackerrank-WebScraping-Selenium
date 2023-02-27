import { Component } from '@angular/core';

@Component({
  selector: 'app-hackerrank-plagiarism-check',
  templateUrl: './hackerrank-plagiarism-check.component.html',
  styleUrls: ['./hackerrank-plagiarism-check.component.scss']
})
export class HackerrankPlagiarismCheckComponent {
  username$ !: string;
  password$ !: string;
  contestName$ !: string;

  fetchUsersData(){
    
  }
}
