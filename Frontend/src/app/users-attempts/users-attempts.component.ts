import { Component } from '@angular/core';
import { ContentServiceService } from '../content-service.service';
@Component({
  selector: 'app-users-attempts',
  templateUrl: './users-attempts.component.html',
  styleUrls: ['./users-attempts.component.scss']
})
export class UsersAttemptsComponent{
    userPlagiarism$: any;
    constructor(private contentService: ContentServiceService){
      this.userData$ = this.contentService.fetch_old_attempts();
    }

    
    userData$: any;
    fetchLatestUsersData(){
      this.userData$ = this.contentService.fetch_latest_attempts();
      console.log(this.userData$);
    }
    handleButtonClick(username: string) {
      // Handle the button click event here
      this.userPlagiarism$ = this.contentService.checkPlagiarism(username);
      // console.log('Selected username:', username);
    }
    // applyFilter(e:any) {
    //   let filterValue = e.target.value;
    //   this.dataSource.filter = filterValue.trim().toLowerCase();
  
    //   if (this.dataSource.paginator) {
    //     this.dataSource.paginator.firstPage();
    //   }
    // }
  
  


}
