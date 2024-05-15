#include "phylib.h"

//creates a new still ball
phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos ){
  
  phylib_object * newBall = NULL;

  newBall = malloc(sizeof(phylib_object));

  if(newBall != NULL){
    
    newBall->type = 0;
    newBall->obj.still_ball.pos.x = (*pos).x; 
    newBall->obj.still_ball.pos.y = (*pos).y; 
    newBall->obj.still_ball.number = number;
    
  }

  return newBall;
}

//creates a new rolling ball
phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc ){

  phylib_object * newBall = NULL;

  newBall = malloc(sizeof(phylib_object));

  if(newBall != NULL){
    
    newBall->type = 1;
    newBall->obj.rolling_ball.pos.x = (*pos).x; 
    newBall->obj.rolling_ball.pos.y = (*pos).y; 
    newBall->obj.rolling_ball.number = number;
    newBall->obj.rolling_ball.vel.x = (*vel).x; 
    newBall->obj.rolling_ball.vel.y = (*vel).y;
    newBall->obj.rolling_ball.acc.x = (*acc).x; 
    newBall->obj.rolling_ball.acc.y = (*acc).y;
    
  }

  return newBall;
}

//creates a new hole
phylib_object *phylib_new_hole( phylib_coord *pos ){
  
  phylib_object * newHole = NULL;
  
  newHole = malloc(sizeof(phylib_object));

  if(newHole != NULL){
    
    newHole->type = 2;
    newHole->obj.hole.pos.x = (*pos).x; 
    newHole->obj.hole.pos.y = (*pos).y; 
    
  }

  return newHole;
}

//creates a new hcushion
phylib_object *phylib_new_hcushion( double y ){
  
  phylib_object * newHCushion = NULL;

  newHCushion = malloc(sizeof(phylib_object));

  if(newHCushion != NULL){
    
    newHCushion->type = 3;
    newHCushion->obj.hcushion.y = y;
    
  }
  
  return newHCushion;
}

//creates a new vcushion
phylib_object *phylib_new_vcushion( double x ){
  
  phylib_object * newVCushion = NULL;

  newVCushion = malloc(sizeof(phylib_object));

  if(newVCushion != NULL){
    
    newVCushion->type = 4;
    newVCushion->obj.vcushion.x = x;
    
  }

  return newVCushion;
}

//creates a new table
phylib_table *phylib_new_table( void ){

  phylib_table * newTable = NULL;

  newTable = malloc(sizeof(phylib_table));

  for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
    newTable->object[i] = NULL;
  }

  if(newTable != NULL){
    
    //set up time
    newTable->time = 0.0;
    (*newTable->object) = NULL;

    //create cushions
    phylib_add_object(newTable, phylib_new_hcushion(0.0));
    phylib_add_object(newTable, phylib_new_hcushion(PHYLIB_TABLE_LENGTH));
    phylib_add_object(newTable, phylib_new_vcushion(0.0));
    phylib_add_object(newTable, phylib_new_vcushion(PHYLIB_TABLE_WIDTH));

    //create holes using a loop and a fun equation i made
    // for(int n = 0; n < 6; n++){
      
    //   phylib_coord pos;

    //   pos = phylib_new_coord(0, 0);
      
    //   pos.x = (n%2) * PHYLIB_TABLE_WIDTH;
    //   pos.y = PHYLIB_TABLE_LENGTH * (0.5 * ((n/2) - ((n/2)%1)));

    //   phylib_add_object(newTable, phylib_new_hole((&pos)));
    // }

    phylib_coord pos;
    //1
    pos = phylib_new_coord(0, 0);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    //2
    pos = phylib_new_coord(0, 1350);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    //3
    pos = phylib_new_coord(0, 2700);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    //4
    pos = phylib_new_coord(1350, 0);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    //5
    pos = phylib_new_coord(1350, 1350);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    //6
    pos = phylib_new_coord(1350, 2700);
    phylib_add_object(newTable, phylib_new_hole(&pos));
    
  }

  return newTable;
}

//copy any src object to dest
void phylib_copy_object( phylib_object **dest, phylib_object **src ){

  if(src != NULL && *src != NULL && dest != NULL){

    *dest = malloc(sizeof(phylib_object));
    
    if(*dest == NULL){
      return;
    }
    
    memcpy(*dest, *src, sizeof(phylib_object));
  }
}

//copies an entire table with its objects
phylib_table *phylib_copy_table( phylib_table *table ){

  phylib_table * newTable = NULL;
  
  if(table != NULL){

    newTable = malloc(sizeof(phylib_table));
    
    if(newTable != NULL){
      
      memcpy(newTable, table, sizeof(phylib_table));

      newTable->time = table->time;
      
      for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        
        newTable->object[i] = NULL;
        
        if(table->object[i] != NULL){
          
          newTable->object[i] = malloc(sizeof(phylib_object));
          
          if(newTable->object[i] != NULL){
            
            memcpy(newTable->object[i], table->object[i], sizeof(phylib_object));
          }
        }
      }
    }
  }

  return newTable;
}

//adds an object to a given table
void phylib_add_object( phylib_table *table, phylib_object *object ){

  int i = 0;

  while(table->object[i] != NULL && i < PHYLIB_MAX_OBJECTS){
    i++;
  }

  if(i < PHYLIB_MAX_OBJECTS){
    table->object[i] = object;
  }
}

//frees a table
void phylib_free_table( phylib_table *table ){

  if(table != NULL){
    
    for(int n = PHYLIB_MAX_OBJECTS - 1; n >= 0; n--){
      if(table->object[n] != NULL){

        free(table->object[n]);
        table->object[n] = NULL;
      }
    }

    free(table);
  }
}

//subtracts two vectors
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

  phylib_coord sub = phylib_new_coord(c1.x-c2.x, c1.y-c2.y);

  return sub;
}

//calculates length of two vectors
double phylib_length( phylib_coord c ){

  double length = (c.x * c.x) + (c.y * c.y);

  length = sqrt(length);

  return length;
}

//calculates dot product
double phylib_dot_product( phylib_coord a, phylib_coord b ){

  return (a.x * b.x) + (a.y * b.y);
}

//calculates distance between two objects
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

  double distance = -1.0;

  if(obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL){
    return -1.0;
  }

  //switch for cases
  switch(obj2->type){

    //still
    case PHYLIB_STILL_BALL:

      distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos));

      distance = distance - (PHYLIB_BALL_RADIUS * 2);

      break;

    //rolling
    case PHYLIB_ROLLING_BALL:

      distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos));

      distance = distance - (PHYLIB_BALL_RADIUS * 2);

      break;

    //hole
    case PHYLIB_HOLE:

      distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos));

      distance = distance - PHYLIB_HOLE_RADIUS;

      break;

    //hcushion
    case PHYLIB_HCUSHION:

      distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

      break;
    
    //vcushion
    case PHYLIB_VCUSHION:

      distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

      break;
    
  }

  return distance;
}

//Roll a ball for one frame
void phylib_roll( phylib_object * newObject, phylib_object *oldObject, double time ){

  if(newObject == NULL || oldObject == NULL){
    return;
  }

  if(newObject->type != PHYLIB_ROLLING_BALL || oldObject->type != PHYLIB_ROLLING_BALL){
    return;
  }

  //lots of math
  newObject->obj.rolling_ball.pos.x = (oldObject->obj.rolling_ball.pos.x) +
                                      (oldObject->obj.rolling_ball.vel.x * time) +
                                      (0.5 * oldObject->obj.rolling_ball.acc.x * time * time);

  newObject->obj.rolling_ball.pos.y = (oldObject->obj.rolling_ball.pos.y) +
                                      (oldObject->obj.rolling_ball.vel.y * time) +
                                      (0.5 * oldObject->obj.rolling_ball.acc.y * time * time);

  newObject->obj.rolling_ball.vel.x = oldObject->obj.rolling_ball.vel.x + (oldObject->obj.rolling_ball.acc.x * time);

  newObject->obj.rolling_ball.vel.y = oldObject->obj.rolling_ball.vel.y + (oldObject->obj.rolling_ball.acc.y * time);
    
  if(checkSign(newObject->obj.rolling_ball.vel.x, oldObject->obj.rolling_ball.vel.x) == 1){
    newObject->obj.rolling_ball.vel.x = 0;
    newObject->obj.rolling_ball.acc.x = 0;
  }

  if(checkSign(newObject->obj.rolling_ball.vel.y, oldObject->obj.rolling_ball.vel.y) == 1){
    newObject->obj.rolling_ball.vel.y = 0;
    newObject->obj.rolling_ball.acc.y = 0;
  }
}

//checks if a rolling ball should be considered stopped, if it is we make it still
unsigned char phylib_stopped( phylib_object *object ){

  double px, py;
  unsigned char num;

  if(object == NULL || object->type != PHYLIB_ROLLING_BALL){
    return 0;
  }

  px = object->obj.rolling_ball.pos.x;
  py = object->obj.rolling_ball.pos.y;
  num =  object->obj.rolling_ball.number;
  
  if(phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON){
    object->type = PHYLIB_STILL_BALL;
    object->obj.still_ball.pos.x = px;
    object->obj.still_ball.pos.y = py;
    object->obj.still_ball.number = num;
    return 1;
  }

  return 0;
}

//calculates change in velocity and acceleration if a rolling ball collides with any object
void phylib_bounce( phylib_object **a, phylib_object **b ){

  if((*a) == NULL || (*b) == NULL || (*a)->type != PHYLIB_ROLLING_BALL){
    return;
  }

  double px, py;

  unsigned char num;

  //switch for each thing 'a' can collide with
  switch ((*b)->type){

    case PHYLIB_HCUSHION:

      (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
      (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);

      break;

    case PHYLIB_VCUSHION:

      (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
      (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);

      break;

    case PHYLIB_HOLE:

      free((*a));

      *a = NULL;

      break;

    case PHYLIB_STILL_BALL:

      px = (*b)->obj.still_ball.pos.x;
      py = (*b)->obj.still_ball.pos.y;
      num = (*b)->obj.still_ball.number;

      (*b)->type = PHYLIB_ROLLING_BALL;

      (*b)->obj.rolling_ball.pos.x = px;
      (*b)->obj.rolling_ball.pos.y = py;
      (*b)->obj.rolling_ball.number = num;
      (*b)->obj.rolling_ball.vel.x = 0.0;
      (*b)->obj.rolling_ball.vel.y = 0.0;
      (*b)->obj.rolling_ball.acc.x = 0.0;
      (*b)->obj.rolling_ball.acc.y = 0.0;

    //if its a rolling ball lots of math
    case PHYLIB_ROLLING_BALL:{
      
      //1
      phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

      //2
      phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

      //3
      phylib_coord n;
      
      if(phylib_length(r_ab) != 0){
        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);
      }else{
        n.x = 0;
        n.y = 0;
      }

      //4
      double v_rel_n = phylib_dot_product(v_rel, n);

      //5
      (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
      (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

      //6
      (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
      (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

      if(phylib_length((*a)->obj.rolling_ball.vel) > PHYLIB_VEL_EPSILON){
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / phylib_length((*a)->obj.rolling_ball.vel) * PHYLIB_DRAG;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / phylib_length((*a)->obj.rolling_ball.vel) * PHYLIB_DRAG;
      }

      if(phylib_length((*b)->obj.rolling_ball.vel) > PHYLIB_VEL_EPSILON){
        (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / phylib_length((*b)->obj.rolling_ball.vel) * PHYLIB_DRAG;
        (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / phylib_length((*b)->obj.rolling_ball.vel) * PHYLIB_DRAG;
      }

      break;
    }
  }
}

//check how many balls are rolling at a given frame
unsigned char phylib_rolling( phylib_table *t ){
  
  unsigned char numRollingBalls = 0;

  if(t == NULL){
    return 0;
  }
  
  for(int n = 0; n < PHYLIB_MAX_OBJECTS; n++){
    if(t->object[n] != NULL && t->object[n]->type == PHYLIB_ROLLING_BALL){
      numRollingBalls++;
    }
  }
  return numRollingBalls;
}

//rolls ball until a bounce or stop happens. (or run out of time)
phylib_table *phylib_segment( phylib_table *table ){

  unsigned char stopped = 0;

  int time = 1;

  //make a hit table to make sure balls do not collide twice in one frame
  int hit[26] = {0};

  if(table == NULL){
    return NULL;
  }
  
  if(phylib_rolling(table) == 0){
    return NULL;
  }
  
  phylib_table * newTable = phylib_copy_table(table);

  if(newTable == NULL){
    return NULL;
  }

  //while no events and max time is not elapsed//
  while(time * PHYLIB_SIM_RATE < PHYLIB_MAX_TIME && stopped == 0){

    //move all objects
    for(int n = 0; n < PHYLIB_MAX_OBJECTS; n++){
      
      if(table->object[n] != NULL && table->object[n]->type == PHYLIB_ROLLING_BALL){
        
        phylib_roll(newTable->object[n], table->object[n], time * PHYLIB_SIM_RATE);
          
      }
    }

    //check for collisons between objects
    for(int n = 0; n < PHYLIB_MAX_OBJECTS; n++){
      for(int n2 = 0; n2 < PHYLIB_MAX_OBJECTS; n2++){
        //if an object is a rolling ball and is not colliding with itself and both objects can be hit then bounce the two objects
        if(newTable->object[n] != NULL && newTable->object[n]->type == PHYLIB_ROLLING_BALL && newTable->object[n2] != NULL 
          && phylib_distance(newTable->object[n], newTable->object[n2]) < 0.0 && n != n2 && hit[n] == 0 && hit[n2] == 0){  

          phylib_bounce(&newTable->object[n], &newTable->object[n2]);

          //mark an event has occured
          stopped = 1;

          //mark the rolling ball to not be hit again on this frame
          hit[n] = 1;

          //do same for object two given it is a rolling ball
          if(newTable->object[n2]->type == PHYLIB_ROLLING_BALL){
            hit[n2] = 1;
          }
          
        }

        //if a ball has stopped mark an event
        if(phylib_stopped(newTable->object[n]) == 1){
          stopped = 1;
        }   
        
      }

     
      
    }

    //increment time
    if(stopped != 1){
      time += 1;
    }
  }

  //add to time to new table
  newTable->time += time * PHYLIB_SIM_RATE;
  
  return newTable;
}

//help to make a new coord
phylib_coord phylib_new_coord(double x, double y){
  
  phylib_coord newCoord;

  //newCoord = malloc(sizeof(phylib_coord));

  //if(newCoord != NULL){
    
    newCoord.x = x;

    newCoord.y = y;
  //}

  return newCoord;
}

//check signs match
int checkSign (double newV, double oldV){
  
  if( (newV > 0 && oldV > 0) || (newV < 0 && oldV < 0) ){
    return 0;
  }
  
  return 1;
}

//Profs Work
void phylib_print_object( phylib_object *object )
{
  if (object==NULL)
  {
    printf( "NULL;\n" );
    return;
  }

  switch (object->type)
  {
    case PHYLIB_STILL_BALL:
      printf( "STILL_BALL (%d,%6.1lf,%6.1lf)\n",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
      break;

    case PHYLIB_ROLLING_BALL:
      printf( "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)\n",
              object->obj.rolling_ball.number,
              object->obj.rolling_ball.pos.x,
              object->obj.rolling_ball.pos.y,
              object->obj.rolling_ball.vel.x,
              object->obj.rolling_ball.vel.y,
              object->obj.rolling_ball.acc.x,
              object->obj.rolling_ball.acc.y );
      break;

    case PHYLIB_HOLE:
      printf( "HOLE (%6.1lf,%6.1lf)\n",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
      break;

    case PHYLIB_HCUSHION:
      printf( "HCUSHION (%6.1lf)\n",
        object->obj.hcushion.y );
      break;

    case PHYLIB_VCUSHION:
      printf( "VCUSHION (%6.1lf)\n",
        object->obj.vcushion.x );
      break;
  }
}

//Profs Work
void phylib_print_table( phylib_table *table )
{
  if (!table)
  {
    printf( "NULL\n" );
    return ;
  }

  printf( "time = %6.4lf;\n", table->time );
  for ( int i=0; i<PHYLIB_MAX_OBJECTS; i++ )
  {
    printf( "  [%02d] = ", i );
    phylib_print_object( table->object[i] );
  }

}

//Profs Work
char *phylib_object_string( phylib_object *object )
{
  static char string[80];
  
  if (object==NULL){
    snprintf( string, 80, "NULL;" );
    return string;
  }
  
  switch (object->type){
  
    case PHYLIB_STILL_BALL:
      snprintf( string, 80,"STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
      break;
    
    case PHYLIB_ROLLING_BALL:
      snprintf( string, 80,"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
        object->obj.rolling_ball.number,
        object->obj.rolling_ball.pos.x,
        object->obj.rolling_ball.pos.y,
        object->obj.rolling_ball.vel.x,
        object->obj.rolling_ball.vel.y,
        object->obj.rolling_ball.acc.x,
        object->obj.rolling_ball.acc.y );
      break;
    
    case PHYLIB_HOLE:
      snprintf( string, 80, "HOLE (%6.1lf,%6.1lf)",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
      break;
    
    case PHYLIB_HCUSHION:
      snprintf( string, 80,"HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
      break;
    
    case PHYLIB_VCUSHION:
      snprintf( string, 80,"VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
  }
  
  return string;
}
