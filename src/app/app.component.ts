import { Component } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  data: Array<{offerId: string, status: string}> = [];
  title = 'webangular';
  constructor(private socket: Socket) { }

  ngOnInit() {
    this.socket.on('topico', (data: Array<{offerId: string, status: string}>) => {
      console.log(data);
      this.data = data;
    });
 
    this.socket.emit('subscribe', { topic: 'topico' });
  }
}
