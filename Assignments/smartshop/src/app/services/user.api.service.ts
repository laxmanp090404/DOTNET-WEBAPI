import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { LoginModel } from "../models/login.model";
import { baseUrl } from "../../environment";

@Injectable({
  providedIn: 'root'
})
export class UserApiService {
  
  constructor(private http: HttpClient
  ) { }
  public loginApiCall(loginData: LoginModel) {
    let url = baseUrl + '/auth/login';
    return this.http.post(url, loginData);
  }
}