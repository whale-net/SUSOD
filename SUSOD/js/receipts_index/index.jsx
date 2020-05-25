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



class Index extends Component {

	constructor() {
		super();
		this.state = {
			Description: '',
			ShowModal: false, 
			ReceiptID: 0
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

		this.handleModalClose = this.handleModalClose.bind(this);
		this.handleModalSave = this.handleModalSave.bind(this);

		this.componentDidMount = this.componentDidMount.bind(this);
		this.onReceiptClick = this.onReceiptClick.bind(this);
		this.onSearch = this.onSearch.bind(this);
	}

	onReceiptClick(e) {

		this.setState({ShowModal: true, ReceiptID: e.target.textContent });
		console.log(e.target.textContent);
	}

	onDescriptionChange(e) {
		this.setState({Description: e.target.value});
	}
	
	componentDidMount() {

		fetch(this.props.url + 'setup', { credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				console.log(data);
				this.setState({data: data});
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
		this.setState({ShowModal: false, ReceiptID: 0});
	}

	handleModalSave(e) {
		console.log('hi')
		this.setState({ShowModal: false,ReceiptID: 0});		
	}


	render() {
		return (

			<div>
				<Modal
		          isOpen={this.state.ShowModal}
		          // onAfterOpen={}
		          contentLabel="Example Modal"
		        >
		        	<Receipt url={this.props.url + 'receipt'} id={parseInt(this.state.ReceiptID)} />
		          	<Button variant='primary' onClick={this.handleModalClose}>Close</Button>

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
									</Form.Group>
								</Form.Row>
						</Form.Group>
						<Form.Group as={Col} lg={8}>
							
							<Form.Row>
								<Button variant="primary" onClick={this.onSearch} className="mx-auto mt-5">
									Search
								</Button> 
							</Form.Row>
						</Form.Group>
					</Form.Row>
				</Form>

			

				<div style={{overflow:'scroll', height: '400px'}}>
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

				