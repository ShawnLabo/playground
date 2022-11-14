package tube.shawn.java.demo;

import java.util.UUID;
import org.springframework.data.repository.CrudRepository;

// @RepositoryRestResource(collectionResourceRel = "messages", path = "messages")
public interface MessageRepository extends CrudRepository<Message, UUID>{
}
