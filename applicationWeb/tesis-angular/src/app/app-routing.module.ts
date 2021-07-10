import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MainModuleTesisRoutingModule } from './main-module-tesis/main-module-tesis-routing.module'

const routes: Routes = [

  ...MainModuleTesisRoutingModule

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

}
