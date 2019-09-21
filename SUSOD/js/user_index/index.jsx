import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


class Index extends Component {
	constructor() {
		super();
		this.state = {};

		this.onUsernameChange = this.onUsernameChange.bind(this);
	}

	componentDidMount() {
		fetch(this.props.url, { credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState(data);
			});
	}

	onUsernameChange(e) {
		this.setState({FirstName: e.target.value});
	}

	render() {
		return (
			<Row className="border border-dark">
				<Col lg={4}>
						<Row className="border">
							<Col>
								<Image src="https://cdn.bulbagarden.net/upload/thumb/8/87/Sima_Miltank.png/250px-Sima_Miltank.png"  rounded />
							</Col>
						</Row>
						<Row className="border">
							<Col>
								<span >Username: </span>
								<span className="label label-default">
									{this.state.Username}
								</span>
							</Col>
						</Row>
				</Col>
				<Col lg={8}>
					<Row>
						<InputGroup>
							<InputGroup.Prepend>
								<InputGroup.Text>First Name:</InputGroup.Text>
							</InputGroup.Prepend>
							<Form.Control 
								value={!this.state.FirstName ? '' : this.state.FirstName} 
								onChange={this.onUsernameChange}
							/>
						</InputGroup>
					</Row>
					<Row>

					</Row>
				</Col>
			</Row>
		);
	}
}


Index.propTypes = {
	url: PropTypes.string.isRequired,
}


export default Index;