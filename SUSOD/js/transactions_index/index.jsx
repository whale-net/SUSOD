import React, {Component} from 'react';
import PropTypes from 'prop-types';

import memoize from 'memoize-one';
import DataTable from 'react-data-table-component';

import Button from 'react-bootstrap/Button';

class Index extends Component {

	constructor(props){
		super(props);

		this.state = {
			data: {}
		}

		//Describes the columns for this page's grid
		this.columns = [
			{
				name: "TransactionID",
				selector: 'TransactionID', 
				sortable: true,
				button: true,
				//cell: row => <Button raised primary onClick={this.onReceiptClick}>{row.ReceiptID}</Button>
			}, 
			{
				name: 'Sender', 
				selector: 'Sender', 
				sortable: true
			},
			{
				name: 'Receiver',
				selector:'Receiver',
				sortable: true
			},
			{
				name: 'TransactionAmount',
				selector: 'TransactionAmount',
				sortable: true
			},
			{
				name: 'IsReceiverConfirmed',
				selector: 'IsReceiverConfirmed',
				sortable: true,
				cell: (row) =>  { console.log(this.state);if (this.state.data.UserID == row.ReceiverUserID && row.IsReceiverConfirmed == 0) {return <Button raised primary onClick={() => {this.onConfirmSR(row.TransactionID, 'receiver')}}>Confirm</Button>;} else {return row.IsReceiverConfirmed;}}

				// format: format('MMMM Do, YYYY H:mma')
			},
			{
				name: 'IsSenderConfirmed',
				selector: 'IsSenderConfirmed',
				sortable: true,
				cell: (row) =>  { console.log(this.state);if (this.state.data.UserID == row.SenderUserID && row.IsSenderConfirmed == 0) {return <Button raised primary onClick={() => {this.onConfirmSR(row.TransactionID, 'sender')}}>Confirm</Button>;} else {return row.IsSenderConfirmed}}

				// format: format('MMMM Do, YYYY H:mma')
			}
		];

	}


	componentDidMount() {
		this.search();
		 
	}

	onConfirmSR(TransactionID, UserType){
		fetch(this.props.url + 'confirm', 
			{
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify({'SenderReceiver': UserType, 'TransactionID': TransactionID})
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			// .then((data) => {
			// 	this.setState({data: data});
			// })
			.catch((error) => {
				console.log(error);
			});

		this.search();
	}


	search() {
		fetch(this.props.url + 'search', { credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState({data: data});
			})
			.catch((error) => {
				console.log(error);
			});
	}

	render() {
		return (
			<div style={{overflow:'scroll', height: '75vh' }}>
					<DataTable
						title= 'Transactions'
						columns={this.columns}
						data={this.state.data.transactions}
					/>	
				</div>

		);
	}
}

Index.propTypes = {
	url: PropTypes.string.isRequired,
}

export default Index;

				