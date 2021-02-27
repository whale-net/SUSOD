import React, {Component} from 'react';
import PropTypes from 'prop-types';

import memoize from 'memoize-one';
import DataTable from 'react-data-table-component';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Modal from 'react-modal';

import Receipt from './receipt.jsx';
// const data=[{ReceiptID: 1, Description: "This is a test"}];

import {FiSearch, FiPlusCircle} from 'react-icons/fi'



import DatePicker from "react-datepicker";
 
import "react-datepicker/dist/react-datepicker.css";
// import 'react-datepicker/dist/react-datepicker-cssmodules.css'
//icons 
import {FiPlusSquare} from 'react-icons/fi';


class Index extends Component {

	constructor() {
		super();

		this.defaultReceipt = {receipt: {PurchaseDate: new Date(), Amount: null, Description: "", OwnerUserID: null}, users: [], receiptsUsers: {}, userSet: {}}

		this.state = {
			Description: '',
			ShowModal: false, 
			ReceiptID: 0,
			Amount: null,
			OnlyShowUnpaid: false,
			UserID: 0,
			ReceiptData: this.defaultReceipt,
			SuccessMessage: ""
		};

		// Describes the columns for this page's grid
		this.columns = [
			{
				name: "ReceiptID",
				selector: 'ReceiptID', 
				sortable: true,
				button: true,
				cell: row => <Button raised primary onClick={this.onReceiptClick}>{row.ReceiptID}</Button>
			}, 
			{
				name: 'Description', 
				selector: 'Description', 
				sortable: true
			},
			{
				name: 'Amount',
				selector:'Amount',
				sortable: true
			},
			{
				name: 'Username',
				selector: 'Username',
				sortable: true
			},
			{
				name: 'PurchaseDate',
				selector: 'PurchaseDate',
				sortable: true,
				// format: format('MMMM Do, YYYY H:mma')
			}
		];

		this.onDescriptionChange = this.onDescriptionChange.bind(this);
		this.onAmountChange = this.onAmountChange.bind(this);
		this.onOnlyShowUnpaidChange = this.onOnlyShowUnpaidChange.bind(this);
		this.handleModalClose = this.handleModalClose.bind(this);
		this.handleModalSave = this.handleModalSave.bind(this);
		this.componentDidMount = this.componentDidMount.bind(this);
		this.onReceiptClick = this.onReceiptClick.bind(this);
		this.onNewClick = this.onNewClick.bind(this);
		this.onSearch = this.onSearch.bind(this);
		this.updateReceiptFieldIfDefined = this.updateReceiptFieldIfDefined.bind(this);
		//this.onReceiptsUsersChange = this.onReceiptsUsersChange.bind(this);
		this.updateReceiptUsersFieldIfDefined = this.updateReceiptUsersFieldIfDefined.bind(this);
		this.toggleReceiptUserDeleted = this.toggleReceiptUserDeleted.bind(this);
	}

	onReceiptClick(e) {

		fetch(this.props.url + 'receipt', {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(e.target.textContent) // provide the receiptid
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState({ReceiptData: data});
				console.log(this.state);
			})
			.catch((error) => {
				console.log(error);
			});


		this.setState({ShowModal: true, ReceiptID: e.target.textContent });


	}

	// onReceiptsUsersChange(e) {
	// 	let userId = e.target.value;
	// 	// console.log(this.state.receiptsUsers);

	// 	if (document.getElementById(`chk-${userId}`).checked){
	// 		// checkbox is checked..
	// 		if (!this.findByField(this.state.ReceiptData.receiptsUsers, 'UserID', userId)){
	// 			let ReceiptData = this.state.ReceiptData;
	// 			ReceiptData.receiptsUsers.push({'UserID': userId,  'DeductionAmount': 0, 'PaymentRatio': 1});
	// 			this.setState({ReceiptData: ReceiptData});
	// 		}
	// 	}
	// 	else{
	// 		let ReceiptData = this.state.ReceiptData;

	// 		for (var i =0; i < ReceiptData.receiptsUsers.length; i++){
	// 		   if (ReceiptData.receiptsUsers[i]['UserID'] == userId) {
	// 			  ReceiptData.receiptsUsers.splice(i,1);
	// 			  break;
	// 		   }
	// 		}

	// 		this.setState({ReceiptData: ReceiptData});
	// 	}
	// }
	
	// clearReceiptsUsers() {
	// 	console.log(this.state);

	// 	if (!!this.state.ReceiptData.users.length && this.state.ReceiptData.users.length > 0) {

	// 		for (let i = 0; i < this.state.ReceiptData.users.length; i++) {
	// 			let userId = this.state.ReceiptData.users[i].UserID;
	// 			if (userId > 0) {
	// 				let chkbox = document.getElementById(`chk-${userId}`);

	// 				if (chkbox.checked) {
	// 					chkbox.checked = false;
	// 				}

	// 			}
	// 		}
	// 	}
	// 	else {
	// 		// assume hardcoded 
	// 		for (let i = 8; i < 11; i++) {
	// 			let userId = i;
	// 			if (userId > 0) {
	// 				let chkbox = document.getElementById(`chk-${userId}`);

	// 				if (chkbox.checked) {
	// 					chkbox.checked = false;
	// 				}
	// 				onReceiptsUsersChange(i);
	// 			}
	// 		}
	// 	}



	// }
	
	onNewClick(e) {
		fetch(this.props.url + 'receipt', {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(0) // provide 0 so we still get users and such
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				console.log(data);
				this.setState({ReceiptData: data});
			})
			.catch((error) => {
				console.log(error);
			});

		this.setState({ShowModal: true, ReceiptID: 0, SuccessMessage: ""});
	//	this.clearReceiptsUsers();
	}

	onDescriptionChange(e) {
		this.setState({Description: e.target.value});
	}
	onAmountChange(e) {
		this.setState({Amount: e.target.value});
	}
	onOnlyShowUnpaidChange(e) {

		// console.log(e.target.checked);
		this.setState({OnlyShowUnpaid: e.target.checked});
	}
	
	componentDidMount() {

		fetch(this.props.url + 'setup', { credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				// console.log(data);
				this.setState({data: data});
				this.setState({UserID: data['UserID']})
			})
			.catch((error) => {
				console.log(error);
			});
	}

	onSearch(e) {
		fetch(this.props.url + 'search', 
			{
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(this.state)
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				console.log(data);
				this.setState({data: data['data']});
			})
			.catch((error) => {
				console.log(error);
			});
	}

	handleModalClose(e) {
		
		this.setState({ShowModal: false, ReceiptID: 0, SuccessMessage: ""});
	}

	handleModalSave(e) {
		let ReceiptData = this.state.ReceiptData;
		ReceiptData.receipt.PurchaseDate = new Date(ReceiptData.receipt.PurchaseDate); // clean purchasedate

		this.setState({ReceiptData: ReceiptData});

		fetch(this.props.url + 'save', {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(this.state.ReceiptData)
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState({ReceiptData: data, SuccessMessage: "Saved Successfully, ReceiptID: " + data.ReceiptID.toString(), ReceiptID: data.ReceiptID});
				
			})
			.catch((error) => {
				console.log(error);
			});
		// console.log(this.state);
	}

	updateReceiptFieldIfDefined(field, value){
		// console.log(field);
		// console.log(value);
		if (!!this.state.ReceiptData){
			let ReceiptData = this.state.ReceiptData;
			ReceiptData.receipt[field] = value;

			this.setState({ReceiptData: ReceiptData});

		}
	}
	
	updateReceiptUsersFieldIfDefined(field, value, userid){
		if (!!this.state.ReceiptData.receiptsUsers){
			if (!!this.state.ReceiptData.receiptsUsers[userid] && !!this.state.ReceiptData.receiptsUsers[userid][0]){
				let receiptUser = this.state.ReceiptData.receiptsUsers[userid][0];
				receiptUser[field] = value;
				

				let ReceiptData = this.state.ReceiptData;
				ReceiptData.receiptsUsers[userid][0] = receiptUser;
				this.setState({ReceiptData: ReceiptData});

			} else { // create default then call this function again
				let ReceiptData = this.state.ReceiptData;
				let newReceiptUser = {ReceiptUserID: -1, PaymentRatio: 1, DeductionAmount: 0};

				ReceiptData.receiptsUsers[userid] = [];
				ReceiptData.receiptsUsers[userid].push(newReceiptUser);
				
				this.setState({ReceiptData: ReceiptData});
				this.updateReceiptUsersFieldIfDefined(field, value, userid);
			}

		}
		
	}

	toggleReceiptUserDeleted(userid){
		if (!!this.state.ReceiptData.receiptsUsers){
			if (!!this.state.ReceiptData.receiptsUsers[userid] && !!this.state.ReceiptData.receiptsUsers[userid][0]){
				let isDeleted = this.state.ReceiptData.receiptsUsers[userid][0]["Deleted"]
				this.updateReceiptUsersFieldIfDefined("Deleted", !isDeleted, userid);
			}
			else {
				this.updateReceiptUsersFieldIfDefined("Deleted", false, userid);
			}
		}
		console.log(this.state.ReceiptData.receiptsUsers);
	}

	findByField(array, field, value) {
		for(var i = 0; i < array.length; i += 1) {
			if(array[i][field] === value) {
				return array[i];
			}
		}
	}

	render() {
		return (
			<div >
				

				<Modal
					isOpen={this.state.ShowModal}
					// className="ml-5 mt-5 pt-5 pl-5"
					// style={{width: '2px'}}
					// onAfterOpen={}
		        >
		        	<h2>{this.state.ReceiptData.receipt.ReceiptID > 0 ? 'ReceiptID: ' + this.state.ReceiptData.receipt.ReceiptID : "New Receipt"}</h2>
		        	<p>{this.state.SuccessMessage}</p>
					<Form> 
						<Form.Group 
								as={Col} 
								md={12}>
							<Form.Row className="pt-3 ">
								<InputGroup className="col-6">
									<InputGroup.Prepend>
										<InputGroup.Text>Description</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										value={this.state.ReceiptData.receipt.Description}
										onChange={(e) => this.updateReceiptFieldIfDefined('Description', e.target.value)}

									/>
								</InputGroup>
							</Form.Row>
							<Form.Row className='pt-3'>
								<InputGroup className="col-2">
									<InputGroup.Prepend>
										<InputGroup.Text>Amount</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										value={this.state.ReceiptData.receipt.Amount} 
										onChange={(e) => this.updateReceiptFieldIfDefined('Amount', e.target.value)}

										// onChange={(e) => console.log(e)}
									/>
								</InputGroup>
								<InputGroup className="col-3" style={{width: "20em"}}>
									<InputGroup.Prepend>
										<InputGroup.Text>Purchased By</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										as="select" 
										value={this.state.ReceiptData.receipt.OwnerUserID}
										onChange={(e) => this.updateReceiptFieldIfDefined('OwnerUserID', e.target.value)}//this.onOwnerUserIDChange}
										>
							    		{this.state.ReceiptData.users.map((user) => (
							    				<option value={user.UserID}>{user.Username}</option>
						    			))}	
								    </Form.Control>
								</InputGroup>
								<InputGroup className="col-3 ">	
									<InputGroup.Prepend>
										<InputGroup.Text>Purchased Date</InputGroup.Text>
									</InputGroup.Prepend>
									<DatePicker
								        selected={new Date(this.state.ReceiptData.receipt.PurchaseDate.toString())}
								        onChange={(e) => this.updateReceiptFieldIfDefined('PurchaseDate', e)}								
								      />
								</InputGroup>


							</Form.Row>
							<Form.Row className='pt-3'>
								<InputGroup className="">
									
									
									{ !!this.state.ReceiptData.userSet && Object.keys(this.state.ReceiptData.userSet).map((user) => (  
										<div>
											
											<Form.Check 
										        type={'checkbox'}
										        checked={!!this.state.ReceiptData.receiptsUsers[user] && !!this.state.ReceiptData.receiptsUsers[user][0] ? !this.state.ReceiptData.receiptsUsers[user][0]["Deleted"] : false}
										        id={`chk-${user.UserID}`}
										        key={user.UserID}
										        value={user.UserID}
										        label={user.Username}
										        onClick={(e) => this.toggleReceiptUserDeleted( user)}
										      />
											<InputGroup.Text onClick={(e) => this.toggleReceiptUserDeleted( user)}>{!!this.state.ReceiptData.userSet[user] ? this.state.ReceiptData.userSet[user] : ""}</InputGroup.Text>
	
										    <p>DeductionAmount</p>
											<Form.Control 
											value={!!this.state.ReceiptData.receiptsUsers[user] && !!this.state.ReceiptData.receiptsUsers[user][0] ? this.state.ReceiptData.receiptsUsers[user][0]["DeductionAmount"]: 0 } 
											onChange={(e) => this.updateReceiptUsersFieldIfDefined('DeductionAmount', e.target.value, user)}
											/>
											<p>PaymentRatio</p>
											<Form.Control 
											value={!!this.state.ReceiptData.receiptsUsers[user] && !!this.state.ReceiptData.receiptsUsers[user][0] ? this.state.ReceiptData.receiptsUsers[user][0]["PaymentRatio"]: 0 } 
											onChange={(e) => this.updateReceiptUsersFieldIfDefined('PaymentRatio', e.target.value, user)}
											/>
										</div>
							        ))}
								</InputGroup>
							</Form.Row>
							

							<Form.Row className="pt-3" style={{width: "20em"}}>
								 
							</Form.Row>

						
								<Form.Row>
									<Button onClick={(e) => this.handleModalSave(e)} variant="primary" className="mx-auto mt-5">
										Submit
									</Button> 
							
								</Form.Row>
						</Form.Group>
					</Form>
					<Button variant='primary' onClick={this.handleModalClose}>Close</Button>
					<Button variant='primary' onClick={this.onNewClick}>New</Button>

		        </Modal>

				<Form > 
					
					<Form.Row className="">
						<Form.Group 
							as={Col} 
							lg={4}>
								<Form.Row className="p-3">
									<Form.Group as={Col}>
										<InputGroup className="border" >
											<InputGroup.Prepend>
												<InputGroup.Text>
													Description
												</InputGroup.Text>
											</InputGroup.Prepend>
											<Form.Control
												value={!this.state.Description ? '' : this.state.Description} 
												onChange={this.onDescriptionChange}
											/>
										</InputGroup>
										<InputGroup className="border" >
										
											<InputGroup.Prepend>
												<InputGroup.Text>
													Amount
												</InputGroup.Text>
											</InputGroup.Prepend>
											<Form.Control
												value={!this.state.Amount ? '' : this.state.Amount} 
												onChange={this.onAmountChange}
											/>
										</InputGroup>
											
										<Form.Group controlId="formBasicCheckbox">
											<Form.Check 
												type="checkbox" 
												label="Only show unpaid" 
												onChange={this.onOnlyShowUnpaidChange}
											/>
										</Form.Group>

									</Form.Group>
								</Form.Row>
						</Form.Group>
						<Form.Group as={Col} lg={8}>
							
							<Form.Row>
								<Button className='m-4' variant='primary' onClick={this.onSearch}>Search</Button>
								<Button className='m-4' variant='primary' onClick={this.onNewClick}>New</Button>
							</Form.Row>
						</Form.Group>
					</Form.Row>
				</Form>

			

				<div style={{overflow:'scroll', height: '75vh' }}>
					<DataTable
						title= 'Receipts'
						columns={this.columns}
						data={this.state.data}
					/>	
				</div>

			</div>
				

		);
	}
}

Index.propTypes = {
	url: PropTypes.string.isRequired,
}

export default Index;

				