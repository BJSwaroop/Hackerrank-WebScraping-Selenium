import { Component } from '@angular/core';
import { ContentServiceService } from '../content-service.service';

@Component({
  selector: 'app-users-attempts',
  templateUrl: './users-attempts.component.html',
  styleUrls: ['./users-attempts.component.scss']
})
export class UsersAttemptsComponent {
    username$ !: string;
    password$ !: string;
    contestName$ !: string;
    userData$ : any;

    data= {
      username: this.username$,
      password: this.password$,
      contest: this.contestName$
    }
    constructor(private contentService: ContentServiceService) { 
        // this.fetchOldUsersData();
    }
    // fetchOldUsersData(){
    //   this.userData$ = this.contentService.fetch_old_users_data(this.data);
    // }
    // fetchLatestUsersData(){
    //   console.log(this.data);
    //   this.userData$ = this.contentService.fetch_users_data(this.data);
    //   console.log(this.userData$);
    // }
}
