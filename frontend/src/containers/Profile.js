import React from 'react';
import {connect} from 'react-redux';
import {Card, Col, Container, Row, Image} from "react-bootstrap";


const Profile = ({user}) => {

    return (
        <Container>
            <h1 className='mainTitle'>Profile</h1>
            <Row>
                <Col xs={6} md={4}>
                    <Card style={{ width: '17rem'}}>
                        <Image variant="bottom" src={user['avatar']}/>
                    </Card>
                </Col>
                <Col xs={12} md={8}>
                    <Card style={{ width: '33rem' }}>
                        <Card.Body>
                            <Card.Title>{user['username']}</Card.Title><br/>
                            <Card.Subtitle className="mb-2 text-muted">Real name: {user['full_name']}</Card.Subtitle>
                            <Card.Text>
                                Some quick example text to build on the card title and make up the bulk of
                                the card's content.
                            </Card.Text>
                            <Card.Link href={"mailto:" + user['email']}>{user['email']}</Card.Link>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

const mapStateToProps = state => ({
    user: state.authReducer.user
});

export default connect(mapStateToProps)(Profile);
