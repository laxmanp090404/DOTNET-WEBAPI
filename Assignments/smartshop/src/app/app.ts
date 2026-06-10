import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Login } from "./components/login/login";
import { userSubject } from './rxjs/auth.operator';
import { Header } from "./components/header/header";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Login, Header],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  
  protected readonly title = signal('smartshop');
  isLoggedIn = signal(false);

  constructor() {
    userSubject.subscribe({next:(user)=>{
      this.isLoggedIn.set(user!=null);
    }});
  }
}
