import { Component, signal } from '@angular/core';
import { UserModel } from '../../models/user.model';
import { userSubject } from '../../rxjs/auth.operator';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-profile',
  imports: [],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class Profile {
  userData  = signal<UserModel | null>(null);
  private userSubscription?: Subscription;
  constructor(){
    this.userSubscription = userSubject.subscribe(
      {
        next:(user)=>this.userData.set(user)
      }
    );

  }
  onDestroy(){
    this.userSubscription?.unsubscribe();
  }
}
