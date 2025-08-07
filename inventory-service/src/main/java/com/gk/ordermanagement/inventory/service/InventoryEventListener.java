package com.gk.ordermanagement.inventory.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.gk.ordermanagement.common.models.BaseEvent;
import com.gk.ordermanagement.common.models.InventoryFailedEvent;
import com.gk.ordermanagement.common.models.InventoryReservedEvent;
import com.gk.ordermanagement.common.models.OrderPlacedEvent;

@Service
public class InventoryEventListener {

	@Autowired
	private KafkaTemplate<String, BaseEvent> kafkaTemplate;

	private static final Logger logger = LoggerFactory.getLogger(InventoryEventListener.class);

	@KafkaListener(topics = "order-placed", groupId = "inventory-group")
	public void handleOrderPlaced(OrderPlacedEvent event) {
		// Mock stock check
		boolean inStock = true;

		logger.info("[{}] Processing Inventory Event: {}", event.getOrderId(), event.getCustomerId());

		if (inStock) {
			InventoryReservedEvent reservedEvent = new InventoryReservedEvent(event.getOrderId(), inStock);
			kafkaTemplate.send("inventory-reserved", reservedEvent);
		} else {
			kafkaTemplate.send("inventory-failed", new InventoryFailedEvent(event.getOrderId()));
		}
	}
}