import { Component, OnDestroy, signal } from '@angular/core';
import { Subscription } from 'rxjs';
import { userSubject } from '../../rxjs/auth.operator';
import { RouterLink } from "@angular/router";
import { FormField } from "@angular/forms/signals";

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard {
  username = signal('Guest');
  private userSubscription?: Subscription;

  constructor() {
    this.userSubscription = userSubject.subscribe({next:(user)=>{
      this.username.set(user?.username || 'Guest');
    }});
  }

  onDestroy() {
    this.userSubscription?.unsubscribe();
  }
}
