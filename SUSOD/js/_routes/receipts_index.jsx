import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from 'receipts_index/index';



ReactDOM.render(
	<Index url="/api/receipts/" />,
	document.getElementById('reactEntry')
);
				