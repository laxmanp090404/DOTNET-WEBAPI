import { Component, signal } from '@angular/core';
import { logoutUser, userSubject } from '../../rxjs/auth.operator';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-header',
  imports: [RouterLink],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {
  username = signal('Guest');
  private userSubscription?: any;

  constructor() {
    this.userSubscription = userSubject.subscribe({
      next:(user)=>this.username.set(user?.username || 'Guest'),
      error:(error)=>console.error("Error fetching user data", error)
    })
  }
  
  onLogout() {
    logoutUser();
  }
 
  onDestroy() {
    this.userSubscription?.unsubscribe();
  }
}
