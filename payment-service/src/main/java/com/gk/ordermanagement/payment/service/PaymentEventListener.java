package com.gk.ordermanagement.payment.service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.gk.ordermanagement.common.models.BaseEvent;
import com.gk.ordermanagement.common.models.CustomerValidatedEvent;
import com.gk.ordermanagement.common.models.InventoryReservedEvent;
import com.gk.ordermanagement.common.models.PaymentProcessedEvent;

@Service
public class PaymentEventListener {

	private Map<String, Boolean> inventoryStatus = new ConcurrentHashMap<>();
	private Map<String, CustomerValidatedEvent> customerStatus = new ConcurrentHashMap<>();
	
	private static final Logger logger = LoggerFactory.getLogger(PaymentEventListener.class);


	@Autowired
	private KafkaTemplate<String, BaseEvent> kafkaTemplate;

	@KafkaListener(topics = "inventory-reserved", groupId = "payment-group")
	public void onInventoryReserved(InventoryReservedEvent event) {
		logger.info("[{}] Processing Inventory Reserved Event: {}", event.getOrderId(), event);
		inventoryStatus.put(event.getOrderId(), true);
		tryProcessPayment(event.getOrderId());
	}

	@KafkaListener(topics = "customer-validated", groupId = "payment-group")
	public void onCustomerValidated(CustomerValidatedEvent event) {
		logger.info("[{}] Processing Customer Validated Event: {}", event.getOrderId(), event);
		customerStatus.put(event.getOrderId(), event);
		tryProcessPayment(event.getOrderId());
	}

	private void tryProcessPayment(String orderId) {
		if (Boolean.TRUE.equals(inventoryStatus.get(orderId)) && customerStatus.get(orderId) != null) {
			// Process payment
			CustomerValidatedEvent customerEvent = customerStatus.get(orderId);
			kafkaTemplate.send("payment-processed", new PaymentProcessedEvent(orderId, customerEvent.getOrder()));
		}
	}
}
