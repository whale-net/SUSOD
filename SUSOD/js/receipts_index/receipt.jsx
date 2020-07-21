import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import DatePicker from "react-datepicker";
 
import "react-datepicker/dist/react-datepicker.css";
// import 'react-datepicker/dist/react-datepicker-cssmodules.css'
//icons 
import {FiPlusSquare} from 'react-icons/fi';

class Receipt extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			
		};

		this.onReceiptsUsersChange = this.onReceiptsUsersChange.bind(this);
		this.updateReceiptFieldIfDefined = this.updateReceiptFieldIfDefined.bind(this);
		this.saveReceipt = this.saveReceipt.bind(this);
	}

	componentDidMount() {

		console.log('hi');
		fetch(this.props.url, {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(this.props.id)
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState(data);
			})
			.catch((error) => {
				console.log(error);
			});

		 
	}

	// todo this should really be its own component 
	onReceiptsUsersChange(e ) {
		let userId = e.target.value;
		// console.log(this.state.receiptsUsers);

		if (document.getElementById(`chk-${userId}`).checked){
			// checkbox is checked..
			if (!!this.state.receiptsUsers){
				if (!this.findByField(this.state.receiptsUsers, 'UserID', userId)){
					let receiptsUsers = this.state.receiptsUsers;
					receiptsUsers.push({'UserID': userId,  'DeductionAmount': 0, 'PaymentRatio': 1});
					this.setState({receiptsUsers: receiptsUsers});
				}
			}
		}
		else{
			if (!!this.state.receiptsUsers){
				let receiptsUsers = this.state.receiptsUsers;
	
				for (var i =0; i < receiptsUsers.length; i++){
				   if (receiptsUsers[i]['UserID'] == userId) {
					  receiptsUsers.splice(i,1);
					  break;
				   }
				}
	
				this.setState({receiptsUsers: receiptsUsers});
			}
		}
	}

	updateReceiptFieldIfDefined(field, value){
		if (!!this.state.receipt){
			let receipt = this.state.receipt;
			receipt[field] = value;
			console.log(receipt);

			this.setState({receipt: receipt});

		}
	}
	
	saveReceipt (e) {
		// console.log('submit....');
		// modify purchaseDate so format is correct always
		if (!!this.state.receipt)
		{

			let receipt = this.state.receipt;
			receipt.PurchaseDate = new Date(receipt.PurchaseDate); 

			this.setState({receipt: receipt});
			
					fetch(this.props.url + '/save', {
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
							this.setState(data);
							console.log(this.state);
						})
						.catch((error) => {
							console.log(error);
						});
		}

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
			<span>
		{ !!(this.state.receipt) && 
				<div style={{backgroundColor: '#6c757d', width: '26em', justifyContent:'center', alignItems:'center', flexGrow: 1}}>
					<Form> 
						<Form.Group 
								as={Col} 
								md={12}>
							<Form.Row className="pt-3 ">
								<InputGroup className="">
									<InputGroup.Prepend>
										<InputGroup.Text>Description</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										value={this.state.receipt.Description} 
										onChange={(e) => this.updateReceiptFieldIfDefined('Description', e.target.value)}
										placeholder="Description"
									/>
								</InputGroup>
							</Form.Row>
							<Form.Row className="pt-3" >
								<InputGroup style={{width: "20em"}}>
									<InputGroup.Prepend>
										<InputGroup.Text>Amount</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										value={this.state.receipt.Amount} 
										onChange={(e) => this.updateReceiptFieldIfDefined('Amount', e.target.value)}//this.updateReceiptFieldIfDefined(Amount, e)}
										placeholder="Amount"
									/>
								</InputGroup>
								<InputGroup className="pt-3" style={{width: "20em"}}>
									<InputGroup.Prepend>
										<InputGroup.Text>Purchased By</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										as="select" 
										value={this.state.receipt.OwnerUserID}
										onChange={(e) => this.updateReceiptFieldIfDefined('OwnerUserID', e.target.value)}//this.onOwnerUserIDChange}
										>
							    		{this.state.users.map((user) => (
							    				<option value={user.UserID}>{user.Username}</option>
						    			))}	
								    </Form.Control>
								</InputGroup>
							</Form.Row>
								<Form.Row className="pt-3">
									<DatePicker
										style={{width: "20em"}}
								        selected={new Date(this.state.receipt.PurchaseDate.toString())}
								        onChange={(e) => {console.log(e); this.updateReceiptFieldIfDefined('PurchaseDate', e);  }}
								
								      />
							    </Form.Row>
							<Form.Row className='pt-3 '>
								<InputGroup className="">
								{  this.state.users.slice(1).map((user) => (  
									  <Form.Check 
								        type={'checkbox'}
								        checked={this.findByField(this.state.receiptsUsers , 'UserID', user.UserID)}
								        id={`chk-${user.UserID}`}
								        key={user.UserID}
								        value={user.UserID}
								        label={user.Username}
								        onClick={this.onReceiptsUsersChange}
								      />

								        ))}
								</InputGroup>
							</Form.Row>

							<Form.Row className="pt-3" style={{width: "20em"}}>
								 
							</Form.Row>

						
								<Form.Row>
									<Button onClick={this.saveReceipt} variant="primary" className="mx-auto mt-5">
										Submit
									</Button> 
							
								</Form.Row>
						</Form.Group>
					</Form>
				
	  </div>
	}
			</span>)
	}
		  
}


Receipt.propTypes = {
	url: PropTypes.string.isRequired,
	id: PropTypes.number,
	UserID: PropTypes.number,

}


export default Receipt;
