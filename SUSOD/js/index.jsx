import React, {Component} from 'react';
import PropTypes from 'prop-types';




class Index extends Component {
	constructor() {
		super();
		this.state = {
			title: "Test 123"
		};
	}

	componentDidMount() {
		// REST api calls
	}

	render() {
		return (
			<div>
				hello world
			</div>
		);
	}
}


Index.propTypes = {
	url: PropTypes.string.isRequired,
}


export default Index;