import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { baseUrl } from "../../environment";

@Injectable({
    providedIn: 'root'
})
export class ProductApiService {
    constructor(private http: HttpClient) { 

    }
     public getProducts(){
        let url = baseUrl + '/products';
        return this.http.get(url);
     }
     public getProductById(productId: number){
        let url = baseUrl + '/products/' + productId;
        return this.http.get(url);
     }   
};