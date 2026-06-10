import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { Dashboard } from './components/dashboard/dashboard';
import { Products } from './components/products/products';
import { authGuard } from './guards/auth.guard';
import { isLoggedIn } from './rxjs/auth.operator';
import { Profile } from './components/profile/profile';
import { ProductDetails } from './components/product-details/product-details';

export const routes: Routes = [
    {
      path: '',
      redirectTo: ()=>{
        if(isLoggedIn()){
          return '/dashboard';
        }else{
          return '/login';
        } 
      },
      pathMatch: 'full'
    },
    {
        path: 'login',
        component:Login
    },
    {
        path:'dashboard',
        component:Dashboard,
        canActivate: [authGuard]
    },
   {
    path:'products',
    component:Products,
    canActivate:[authGuard]
},
{
    path:'products/:id',
    component:ProductDetails,
    canActivate:[authGuard]
},{
      path:'profile',
      component:Profile,
      canActivate: [authGuard]
    }
];
