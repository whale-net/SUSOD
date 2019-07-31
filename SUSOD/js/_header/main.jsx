import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

// _header


class Header extends Component {
	constructor(props) {
		super(props);
		this.state = {
			
		};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	componentDidMount() {
		// REST api calls
	}

	handleChange(event) {
		this.setSate({

		});
	}

	handleSubmit(event) {
		event.preventDefault();
	}

	render() {
		return (
			<Navbar bg="dark" variant="dark">
				<Navbar.Brand>SUSOD</Navbar.Brand>
				<Nav fill className="mr-auto">
					<Nav.Item>
						<Nav.Link href="">Home</Nav.Link>
					</Nav.Item>
					<Nav.Item>
						<Nav.Link href="">Coffee</Nav.Link>
					</Nav.Item>
					<Nav.Item>
						<Nav.Link href="">Security</Nav.Link>
					</Nav.Item>
					<Nav.Item>
						<Nav.Link href="">Music</Nav.Link>
					</Nav.Item>
					<Nav.Item>
						<Nav.Link href="">Users</Nav.Link>
					</Nav.Item>
				</Nav>
			</Navbar>
		);
	}
}


Header.propTypes = {
}


export default Header;