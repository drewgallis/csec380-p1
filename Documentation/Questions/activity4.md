# Questions - Activity 4

- How do you prevent XSS is this step when displaying the username of the user who uploaded the video?

    *We use a plugin in that is called noscript. What this does is disable all possible execution of javascript functions except for the ones that we have exeptions for.*

- How do you ensure that users can’t delete videos that aren’t their own?

    *When deleting a Video we first do a check in the database to see if they are the owner of the Video. If they are not the owner they cannot delete the video.*