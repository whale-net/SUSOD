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

class Index extends Component {
	constructor() {
		super();
		this.state = {
			arrayvar: [],
			
		};

		this.onServerNameChange = this.onServerNameChange.bind(this);
		this.download = this.download.bind(this);
		this.onSubmit = this.onSubmit.bind(this);
		this.onMapUrlChange = this.onMapUrlChange.bind(this);
		this.onAddMap = this.onAddMap.bind(this);


	}

	componentDidMount() {
		
	}

	download(e) {


	}

	onSubmit(e) {
		var fileData = "[/Script/Pavlov.DedicatedServer]\nbEnabled=true\nMaxPlayers=10\nbSecured=true\n";
		fileData = fileData +'\n' + "ServerName=" + this.state.ServerName + '\n'

		for (var i = 0; i <= this.state.arrayvar.length - 1; i++) {
			fileData += 'MapRotation=(MapId="' + this.state.arrayvar[i].split('=')[1] + '", GameMode="GUN")';
		}


	    var file = new Blob([fileData], {type: 'ini'});
	    if (window.navigator.msSaveOrOpenBlob) // IE10+
	        window.navigator.msSaveOrOpenBlob(file, 'Game.ini');
	    else { // Others
	        var a = document.createElement("a"),
	                url = URL.createObjectURL(file);
	        a.href = url;
	        a.download = 'Game.ini';
	        document.body.appendChild(a);
	        a.click();
	        setTimeout(function() {
	            document.body.removeChild(a);
	            window.URL.revokeObjectURL(url);  
	        }, 0); 
	    }
	}

	onServerNameChange(e) {
		this.setState({ServerName: e.target.value});
	}


	onMapUrlChange(e) {
		this.setState({MapUrl: e.target.value});
	}

	onAddMap(e) {
		this.setState(prevState => ({
		  arrayvar: [...prevState.arrayvar, this.state.MapUrl]
		}));
	}
// array.splice(index, 1);
	onRemoveMap(e) {
		this.setState(prevState => ({
			arrayvar: [...prevState.arrayvar].splice(index, 1)
		}));
	}

	render() {
		return (
			<div>
				<div>
			      {this.state.arrayvar.map((item, index) => (
			        <li>{item}</li>

			      ))}
				</div>
				<Form onSubmit={this.onSubmit}>
					<Form.Group as={Row}>
						<Form.Row >
							<InputGroup className="border">
								<InputGroup.Prepend>
									<InputGroup.Text>
										ServerName
									</InputGroup.Text>
								</InputGroup.Prepend>
								<Form.Control
									value={!this.state.ServerName ? '' : this.state.ServerName}
									onChange={this.onServerNameChange}
									placeholder="ServerName"
								/>

							</InputGroup>
						</Form.Row>
					</Form.Group>
					<Form.Group as={Row	}>

						<Form.Row>
							<InputGroup className="border">
								<InputGroup.Prepend>
									<InputGroup.Text>
										MapUrl
									</InputGroup.Text>
								</InputGroup.Prepend>
								<Form.Control
									value={!this.state.MapUrl ? '' : this.state.MapUrl}
									onChange={this.onMapUrlChange}
									placeholder="https://steamcommunity.com/sharedfiles/filedetails/?id=XXXXXXXXXXX"
								/>

							<Button onClick={this.onAddMap}>
								Add Map 
							</Button>
							</InputGroup>
						</Form.Row>
					</Form.Group>
					<Form.Row>
						<Button variant="primary" type="submit" className="mx-auto mt-5">
							Submit
						</Button> 
					</Form.Row>
				</Form>
			</div>
		);
	}
}

Index.propTypes = {
	url: PropTypes.string.isRequired,
}

export default Index;

				