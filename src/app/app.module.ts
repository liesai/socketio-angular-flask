import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './routing/app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { WishlistComponent } from './services/components/wishlist.components';
import { SocketIoModule, SocketIoConfig  } from 'ngx-socket-io';

const config: SocketIoConfig = { url: 'http://localhost:5000', options: { } };

@NgModule({
  declarations: [
    AppComponent,
    WishlistComponent
  ],
  imports: [
    BrowserModule, AppRoutingModule, HttpClientModule, SocketIoModule.forRoot(config)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }





