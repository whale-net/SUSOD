//https://stackoverflow.com/questions/46119987/upload-and-read-a-file-in-react
import React, {Component} from 'react';
import PropTypes from 'prop-types';




class FileInput extends React.Component {
	constructor(props) {
	  super(props)
	  this.uploadFile = this.uploadFile.bind(this);
	}
	
	uploadFile(event) {
		let file = event.target.files[0];
		if (file) {
			let data = new FormData();
			data.append('file', file);
			//axios.post('/files', data)...
			fetch(this.props.url, {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: multipart/form-data',
				body: data,
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
				console.log('no');
			})
		}
	}
	
	render() {
		return (
			<span>
				<input type="file"
					name="myFile"
					onChange={this.uploadFile} />
			</span>
		)
	}
}


FileInput.propTypes = {
	url: PropTypes.string.isRequired,
}


export default FileInput;
