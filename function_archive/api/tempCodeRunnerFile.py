if response_1[1]['status'] == 2:
    #     print("Error: Cannot delete group owner.")
    #     return {'error': 'Cannot delete group owner.'}

    # # If the member is not the owner, proceed to delete them from the group
    # data, _ = supabase_client.table("Group Members Info").delete()\
    #                 .eq("group_id", group_id)\
    #                 .eq("email", email)\
    #                 .execute()