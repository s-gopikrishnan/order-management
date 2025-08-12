package com.gk.ordermanagement.customer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.gk.ordermanagement.common.models.BaseEvent;
import com.gk.ordermanagement.common.models.CustomerFailedEvent;
import com.gk.ordermanagement.common.models.CustomerValidatedEvent;
import com.gk.ordermanagement.common.models.OrderPlacedEvent;

@Service
public class CustomerEventListener {
	
	@Autowired
	private KafkaTemplate<String, BaseEvent> kafkaTemplate;
	
	private static final Logger logger = LoggerFactory.getLogger(CustomerEventListener.class);

    @KafkaListener(topics = "order-placed", groupId = "customer-group")
    public void handleOrderPlaced(OrderPlacedEvent event) {
        // Validate customer
        boolean isValid = true;
        
		logger.info("[{}] Processing Customer Event: {}", event.getOrderId(), event.getOrder());

        if (isValid) {
            kafkaTemplate.send("customer-validated", new CustomerValidatedEvent(event.getOrderId(), event.getOrder()));
        } else {
            kafkaTemplate.send("customer-failed", new CustomerFailedEvent(event.getOrderId()));
        }
    }
}
