import React, {useState} from 'react';
import {connect} from 'react-redux';
import {Navigate} from 'react-router-dom';
import { useParams } from 'react-router-dom';
import {Button, Col, Container, Row} from "react-bootstrap";
import {verify} from "../actions/authActions";


const Activate = ({verify}) => {

    const [requestSent, setRequestSent] = useState(false);

    const { uid, token } = useParams();

    const verify_account = () => {
        console.log('Verify')
        verify(uid, token);
        setRequestSent(true);
    };

    if (requestSent) {
        return <Navigate to='/signin' />
    }

    return (
        <Container>
            <Row>
                <Col md={{ span: 6, offset: 3 }} className="witeeee">
                    <h1 className='mainTitle'>Verify your account</h1>
                    <div className="mainButton">
                        <Button variant="dark" type="button" onClick={verify_account}>
                            Verify
                        </Button>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default connect(null, {verify})(Activate);
