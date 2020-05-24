import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';

import FileInput from './fileinput';


class Index extends Component {
	constructor() {
		super();
		this.state = {};

		this.onFirstNameChange = this.onFirstNameChange.bind(this);
		this.onLastNameChange = this.onLastNameChange.bind(this);
		this.onSubmit = this.onSubmit.bind(this);
	}

	componentDidMount() {
		fetch(this.props.url, { credentials: 'same-origin'})
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

	onFirstNameChange(e) {
		this.setState({FirstName: e.target.value});
	}

	onLastNameChange(e) {
		this.setState({LastName: e.target.value});
	}

	onSubmit(e) {
		fetch(this.props.url, {
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
			console.log('yay');
		})
		.catch((error) => {
			console.log(error);
			console.log('no');
		})
		e.preventDefault();
	}

	render() {
		return (
			<Form onSubmit={this.onSubmit}>
				<Form.Row className="">
					<Form.Group 
						as={Col} 
						lg={4}>
							<Form.Row className="p-3">
								<Col>
									<Image className="border border-dark" src={this.state.avatar_url}  rounded />
								</Col>
							</Form.Row>
							<Form.Row className="p-3">
								<Form.Group as={Col}>
									<FileInput url={this.props.url + 'avatar'} />
								</Form.Group>
								<Form.Group as={Col}>
									<InputGroup className="border" >
										<InputGroup.Prepend>
											<InputGroup.Text>
												Username
											</InputGroup.Text>
										</InputGroup.Prepend>
										<Form.Control
											defaultValue={this.state.Username}
											disabled={true}
											readOnly={true}
										/>
									</InputGroup>
								</Form.Group>
							</Form.Row>
					</Form.Group>
					<Form.Group as={Col} lg={8}>
						<Form.Row className="pt-3 pb-1 px-2">
							<InputGroup className="">
								<InputGroup.Prepend>
									<InputGroup.Text>First Name</InputGroup.Text>
								</InputGroup.Prepend>
								<Form.Control 
									value={!this.state.FirstName ? '' : this.state.FirstName} 
									onChange={this.onFirstNameChange}
									placeholder="First Name"
								/>
							</InputGroup>
						</Form.Row>
						<Form.Row className="py-1 px-2">
							<InputGroup className="">
								<InputGroup.Prepend>
									<InputGroup.Text>Last Name</InputGroup.Text>
								</InputGroup.Prepend>
								<Form.Control 
									value={!this.state.LastName ? '' : this.state.LastName} 
									onChange={this.onLastNameChange}
									placeholder="Last Name"
								/>
							</InputGroup>
						</Form.Row>
						<Form.Row>
							<Button variant="primary" type="submit" className="mx-auto mt-5">
								Submit
							</Button> 
						</Form.Row>
					</Form.Group>
				</Form.Row>
			</Form>
		);
	}
}


Index.propTypes = {
	url: PropTypes.string.isRequired,
}


export default Index;