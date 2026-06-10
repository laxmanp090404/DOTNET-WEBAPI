import { Component, signal } from '@angular/core';
import { LoginModel } from '../../models/login.model';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { form, FormField, minLength, required } from '@angular/forms/signals';
import { UserApiService } from '../../services/user.api.service';
import { changeUser } from '../../rxjs/auth.operator';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [FormsModule, ReactiveFormsModule, FormField],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  loginModel = signal(new LoginModel());
  progress = signal(false);

  constructor(private userApiService: UserApiService, private router: Router) {
  }
  loginForm = form(this.loginModel, (path) => {
    required(path.username, { message: "Username is required" });
    minLength(path.username, 4, { message: "Username must be at least 4 characters long" });
    required(path.password, { message: "Password is required" });
  });
  handleLoginClick() {
    // console.log(this.loginForm());
    if (this.loginForm().invalid()) {
      alert("Please fix the errors in the form before submitting.");
      return;
    }

    this.progress.set(true);
    this.userApiService.loginApiCall(this.loginModel()).subscribe({
      next: (response: any) => {
        // console.log("Login successful", response);
        sessionStorage.setItem('token', response.accessToken);
        loginSuccessAction();
        changeUser();
        this.progress.set(false);

        // changeUser();
        // this.router.navigate(['/home']);
      },
      error: (error: any) => {
        console.error("Login failed", error);
        alert("Login failed. Please try again.");
        this.progress.set(false);
      }
    });

    const loginSuccessAction = () => {

      alert("Login successful!")
      
      this.router.navigate(['/dashboard']);
    }
  }
}
