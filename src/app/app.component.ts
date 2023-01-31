import { Component, Input } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-table-cell',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
  



export class AppComponent {
  
  data: Array<{offerId: string, status: string}> = [];
  title = 'webangular';
  constructor(private http: HttpClient, private socket: Socket) { };
  

  ngOnInit(): void {

  
this.http.get('http://localhost:8080/amq').subscribe((data: any): void => {
    for (const d of data.slice(0, 10)) {
      this.data.push(d);
      console.log('data from http : ' + d)
    }

});


    this.socket.on('topico', (data: Array<{offerId: string, status: string}>) => {
      console.log(data);
      this.data = data;
    });
 
    this.socket.emit('subscribe', { topic: 'topico' });
        // Listen for changes from the backend
    this.listenForChanges().subscribe(updatedData => {
      // Find the cell with the updated data and update its status
      const cellToUpdate = this.data.find(cell => cell.offerId === updatedData.offerId);
      cellToUpdate.status = updatedData.status ; //REVISER
    });
  }

  listenForChanges(): Observable<{offerId: string, status: string}> {
    // Code to listen for changes from the backend
    return Observable; //REVISER
  }



}
  
@Component({
  selector: 'app-table-cell',
  template: '<td>{{ offerId }}</td><td>{{ status }}</td>',
})
export class TableCellComponent {
  @Input() offerId: string | undefined;
  @Input()
  status!: string;
}

