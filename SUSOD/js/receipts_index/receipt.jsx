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
			UserID: 0,
			receipt: {},
			users: [],
			receiptsUsers: []
		}

		this.onDescriptionChange = this.onDescriptionChange.bind(this);
		this.onAmountChanged = this.onAmountChanged.bind(this);
		this.saveReceipt = this.saveReceipt.bind(this);	  
		this.onOwnerUserIDChange = this.onOwnerUserIDChange.bind(this);
		this.onPurchaseDateChange = this.onPurchaseDateChange.bind(this);
		this.onReceiptsUsersChange = this.onReceiptsUsersChange.bind(this);
	}
	
	componentDidMount() {
		this.setState({UserID: this.props.UserID});
		

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

				this.setState({receipt: data['receipt'][0]});
				this.setState({users: data['users']});
				this.setState({receiptsUsers: data['receiptsUsers']});
				// console.log(this.props.url);
				console.log(data)		

			})
			.catch((error) => {
				console.log(error);
			});

	}

	onReceiptsUsersChange(e ) {
		let userId = e.target.value;
		console.log(this.state.receiptsUsers);

		if (document.getElementById(`chk-${userId}`).checked){
			// checkbox is checked..
			if (!this.findByField(this.state.receiptsUsers, 'UserID', userId)){

				let receiptsUsers = this.state.receiptsUsers;
				receiptsUsers.push({'UserID': userId,  'DeductionAmount': 0, 'PaymentRatio': 1});
				this.setState({receiptsUsers: receiptsUsers});
			}
		}
		else{
			let receiptsUsers = this.state.receiptsUsers;

			for (var i =0; i < receiptsUsers.length; i++){
			   if (receiptsUsers[i]['UserID'] == userId) {
			      receiptsUsers.splice(i,1);
			      break;
			   }
			}

			this.setState({receiptsUsers: receiptsUsers});
		}

		console.log(this.state.receiptsUsers);

		// if (!this.findByField(this.state.receiptsUsers, 'UserID', userId):


	}

	onPurchaseDateChange(e) {
		console.log(e);

		let receipt = this.state.receipt;
		receipt.PurchaseDate = e;
		this.setState({receipt: receipt});
	}

	onDescriptionChange(e) {
		let receipt = this.state.receipt;
		receipt.Description = e.target.value;

		this.setState({receipt: receipt});
		
	}

	onOwnerUserIDChange(e) {
		let receipt = this.state.receipt;
		receipt.OwnerUserID = e.target.value;

		this.setState({receipt: receipt})
	}

	onAmountChanged(e) {
		let receipt = this.state.receipt;
		receipt.Amount = e.target.value;
		
		this.setState({receipt: receipt});
	}

	saveReceipt (e) {
		// console.log('submit....');
		// modify purchaseDate so format is correct always
		let receipt = this.state.receipt;
		receipt.PurchaseDate = new Date(receipt.PurchaseDate); 

		this.setState({receipt: receipt});

		fetch(this.props.url + '/save', {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(this.state)
			})
			// .then((response) => {
			// 	if (!response.ok) throw Error(response.statusText);
			// 	return response.json();
			// })
			.then((data) => {

				this.setState(data);
			})
			.catch((error) => {
				console.log(error);
			});
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
				<div style={{backgroundColor: '#6c757d'}}>
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
										value={!this.state.receipt.Description ? '' : this.state.receipt.Description} 
										onChange={this.onDescriptionChange}
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
										value={!this.state.receipt.Amount ? '' : this.state.receipt.Amount} 
										onChange={this.onAmountChanged}
										placeholder="Amount"
									/>
								</InputGroup>
								<InputGroup className="pl-5" style={{width: "20em"}}>
									<InputGroup.Prepend>
										<InputGroup.Text>Purchased By</InputGroup.Text>
									</InputGroup.Prepend>
									<Form.Control 
										as="select" 
										value={this.state.receipt.OwnerUserID}
										onChange={this.onOwnerUserIDChange}
										>
							    		{this.state.users.map((user) => (
							    				<option value={user.UserID}>{user.Username}</option>
						    			))}	
								    </Form.Control>
								</InputGroup>
							</Form.Row>


							<Form.Row className='pt-3 '>
								<InputGroup className="">
								{this.state.users.slice(1).map((user) => (
									  <Form.Check 
								        type={'checkbox'}
								        checked={this.findByField(this.state.receiptsUsers, 'UserID', user.UserID)}
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
				<div>
					<DatePicker
						style={{width: "20em"}}
				        selected={!!this.state.receipt.PurchaseDate ?  new Date(this.state.receipt.PurchaseDate.toString()): new Date()}
				        onChange={this.onPurchaseDateChange}
				
				      />
				</div>
			</span>
		)
	}
}


Receipt.propTypes = {
	url: PropTypes.string.isRequired,
	id: PropTypes.number,
	UserID: PropTypes.number

}


export default Receipt;
