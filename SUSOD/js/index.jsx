import React, {Component} from 'react';
import PropTypes from 'prop-types';




class Index extends Component {
	constructor() {
		super();
		this.state = {
			
		};
	}

	componentDidMount() {
		// REST api calls
	}

	render() {
		return (
			<div>
				<p>
					Hello World
				</p>
			</div>
		);
	}
}


Index.propTypes = {
	url: PropTypes.string.isRequired,
}


export default Index;