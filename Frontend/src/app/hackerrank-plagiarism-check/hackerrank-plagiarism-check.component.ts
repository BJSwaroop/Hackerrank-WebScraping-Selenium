import { Component } from '@angular/core';
import { ContentServiceService } from '../content-service.service';

@Component({
  selector: 'app-hackerrank-plagiarism-check',
  templateUrl: './hackerrank-plagiarism-check.component.html',
  styleUrls: ['./hackerrank-plagiarism-check.component.scss']
})
export class HackerrankPlagiarismCheckComponent {
  username$ !: string;
  password$ !: string;
  contestName$ !: string;
  userData$ : any;
  constructor(private contentService: ContentServiceService) { 
    
  }
  data:any
  fetchUsersData(){
    this.data = {
      username: this.username$,
      password: this.password$,
      contest: this.contestName$
    }
    console.log(this.data);
    this.userData$ = this.contentService.fetch_users_data(this.data);
    console.log(this.userData$);
  }
}
